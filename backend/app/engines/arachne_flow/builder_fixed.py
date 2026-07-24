        def resolve(raw_id: str, role: str) -> str:
            if raw_id in dual_ids:
                return raw_id
            if role == "target" and pred in input_roles:
                return f"{flow_id}:{raw_id}"
            if role == "source" and pred in output_roles:
                return f"{flow_id}:{raw_id}"
            if role == "target" and pred in output_roles:
                return raw_id
            if role == "source" and pred in input_roles:
                return raw_id
            if pred == SpecialRole.NEXT.value:
                return f"{flow_id}:{raw_id}"
            if pred == SpecialRole.REF.value and role == "source":
                return f"{flow_id}:{raw_id}"
            return raw_id
