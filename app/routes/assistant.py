from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from app.services.gemini_service import ask_gemini

assistant_bp = Blueprint(
    "assistant",
    __name__,
    url_prefix="/assistant"
)


@assistant_bp.route("/")
def index():

    return render_template(
        "assistant/index.html"
    )


@assistant_bp.route("/ask", methods=["POST"])
def ask():

    try:

        question = request.form.get(
            "question",
            ""
        ).strip()

        if not question:

            return jsonify({

                "success": False,

                "error": "Please enter a question."

            })

        answer = ask_gemini(question)

        return jsonify({

            "success": True,

            "answer": answer

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500