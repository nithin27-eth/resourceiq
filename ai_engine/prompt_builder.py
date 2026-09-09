def build_prompt(domain: str, data_list: list[dict], user_question: str) -> str:
    """
    Formats SQLite database rows and user question into a strict AI prompt.
    """
    if not data_list:
        return (
            f"You are ResourceIQ AI. The user is asking about the '{domain}' domain, "
            f"but no data has been saved in the database yet.\n\n"
            f"Instruct the user to click the 'Refresh Data' button on the dashboard first.\n\n"
            f"User Question: {user_question}"
        )

    formatted_rows = []
    for idx, row in enumerate(data_list, 1):
        clean_row = {k: v for k, v in row.items() if k != "id"}
        row_str = " | ".join(f"{k}: {v}" for k, v in clean_row.items())
        formatted_rows.append(f"  Record #{idx} -> {row_str}")

    data_block = "\n".join(formatted_rows)

    prompt = f"""You are ResourceIQ, an expert AI resource analyst. Below is REAL operational telemetry data from the '{domain}' domain:

--- START OF DATA ---
{data_block}
--- END OF DATA ---

Based STRICTLY on the data provided above, answer the following question:
"{user_question}"

CRITICAL RULES:
1. Cite EXACT numbers, names, percentages, and metrics from the data.
2. Provide a concrete, actionable recommendation based on the findings.
3. Do NOT make assumptions or hallucinate information not present in the data.
4. Keep the response professional, concise, and structured in 2-4 sentences."""

    return prompt
