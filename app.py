import os
from Chatbot import Chatbot
from VectorStore import VectorStore
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from supabase import create_client

app = Flask(__name__)

load_dotenv()

supabase = create_client(os.getenv('SUPABASE_URL'),
                         os.getenv('SUPABASE_API_KEY'))

vectorstore = VectorStore()
chatbot = Chatbot()

chatbot.create_conversation_chain(vectorstore.get_vectorstore())


@app.route('/doula', methods=["GET"])
def get_doula():
    try:
        ids = request.args.get('ids')
        zip_code = request.args.get('zip')
        doula_type = request.args.get('doula_type')

        print(ids, 'ids')

        if not zip_code:
            return jsonify({"status": "failure", "error": "ZIP code is required"}), 400

        # Parse the 'ids' parameter into a list of integers to exclude
        # This is used if a user requests another 2 doulas
        exclude_ids = [int(i) for i in ids.split(',') if i] if ids else []

        # Define the columns to select based on doula_type
        general_columns = ["id", "name",
                           "location", "service_range", "website", "phone", "doula_training", "type_of_practice", "clients_per_month", "college_education", "special_services_offered", "languages_spoken", "fee_detail", "certifications", "service_area"]
        birth_columns = ["birth_fee",
                         "birth_doula_experience", "home_births", "birth_center_births", "hospital_births_desc", "birth_center_births_desc", "home_births_desc", "hospital_births"]
        postpartum_columns = [
            "postpartum_rate", "postpartum_doula_experience"]

        # Append additional columns based on doula_type
        if doula_type == 'postpartum':
            columns_to_select = general_columns + postpartum_columns
        elif doula_type == 'birth':
            columns_to_select = general_columns + birth_columns

        print(exclude_ids, 'exclude_ids')

        # Fetch doula IDs from the 'doula_zip' table for the given ZIP code, excluding the provided IDs
        query = supabase.table("doula_zip").select(
            "doula_id").eq('zip', zip_code)

        doula_zip_response = query.execute()

        if doula_zip_response.data:
            # Take only 2 doula IDs that are not in the excluded IDs
            doula_ids = [entry['doula_id']
                         for entry in doula_zip_response.data if entry['doula_id'] not in exclude_ids][:2]

            if doula_ids:
                doula_data_response = supabase.table("doula").select(
                    ",".join(columns_to_select)).in_('id', doula_ids).execute()

                return jsonify({"status": "success", "data": doula_data_response.data})
        else:
            return jsonify({"status": "success", "message": "No doulas found for the given ZIP code"})

    except Exception as e:
        print(e, 'error')
        return jsonify({"status": "failure", "error": str(e)}), 500


@app.route('/chat', methods=["POST"])
def chat():
    try:
        # Extract the message from the request body
        data = request.get_json()
        user_question = data.get('content')

        # Handle the user input with the vector store and chatbot
        if user_question:
            response = chatbot.handle_user_input(user_question)

            # Return the AI response to the user
            return jsonify({"status": "Success", "message": response})
        else:
            return jsonify({"status": "failure", "error": "Missing 'message' parameter in the request body"})

    except Exception as e:
        print(e, 'error')
        return jsonify({"status": "failure", "error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
