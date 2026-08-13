def extract_langpro_prediction(proofs: dict) -> str:
    """
    LangPro's prediction can be deduced from the `info` field of each proof type.

    Expected input (`proofs`):

    ```
    {
        "contradiction": {
            "info": ["na", "open", "Ter", 16],
            "proof": {...}
        },
        "entailment": {
            "info": ["al", "closed", "Ter", 8],
            "proof": {...}
        }
    }
    ```

    Output: "entailment", "contradiction", "neutral", "conflict" or "unknown".


    The `entailment` and `contradiction` properties in `proofs` can have three
    states: 'open', 'closed' or 'failed'. A proof is considered 'open' if its
    'info' field contains 'open' and mutatis mutandis for 'closed'. If the
    'info' field does not exist or contains neither 'open' nor 'closed', the
    proof is considered 'failed'.

    The overall prediction is determined as follows:

    | Entailment tree | Contradiction tree | Resulting judgement |
    |-----------------|--------------------|---------------------|
    | open or failed  | closed             | Contradiction       |
    | closed          | open or failed     | Entailment          |
    | failed          | failed             | Unknown             |
    | open or failed* | open or failed*    | Neutral             |
    | closed          | closed             | Conflict            |

    *: either Entailment or Contradiction has failed, but not both.

    """
    entailment_info = proofs.get("entailment", {}).get("info", [])
    contradiction_info = proofs.get("contradiction", {}).get("info", [])

    def get_proof_state(info):
        if not info:
            return "failed"
        if "open" in info:
            return "open"
        if "closed" in info:
            return "closed"
        return "failed"

    entailment_state = get_proof_state(entailment_info)
    contradiction_state = get_proof_state(contradiction_info)

    if entailment_state == "closed" and contradiction_state in ["open", "failed"]:
        return "entailment"
    elif contradiction_state == "closed" and entailment_state in ["open", "failed"]:
        return "contradiction"
    elif entailment_state == "failed" and contradiction_state == "failed":
        return "unknown"
    elif entailment_state == "closed" and contradiction_state == "closed":
        return "conflict"
    else:
        return "neutral"
