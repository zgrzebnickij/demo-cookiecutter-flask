guestion_schema = {
    "type" : "object",
    "properties" : {
        "results":{
            "type": "array",
            "items": {
                "type": "object",
                "properties":{
                    "category" : {"type" : "string"},
                    "type" : {"type" : "string"},
                    "difficulty" : {"type" : "string"},
                    "question" : {"type" : "string"},
                    "correct_answer" : {"type" : "string"},
                    "incorrect_answers" : {
                        "type": "array",
                        "items": {"type" : "string"}
                    },
                    "answers" : {
                        "type": "array",
                        "items": {"type" : "string"}
                    },
                    "answer" : {"type" : "string"},
                },
                "required": ["type", "question", "correct_answer", "answer"]
            }
        }
    },
    "required": ["results"]
}