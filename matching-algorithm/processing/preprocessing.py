import pandas as pd


# FIXME: Columns names are copying over but not the data
# TODO: If a user puts an invalid KIN ID, just remove from preferences list and add an additional ID to auto-generate
def process_form_data(form_data_path):
    """
    Process the raw form data into a format that can be used in the Gale-Shapley algorithm,
    accommodating different column setups for mentors and mentees.

    Parameters:
        form_data_path (str): Path to the raw form data CSV file.

    Output:
        A processed CSV file (`processed_data.csv`) containing the data formatted for the Gale-Shapley algorithm.
    """
    # Load the raw form data
    raw_data_df = pd.read_csv(form_data_path)

    # Create a new DataFrame for processed results
    processed_data_df = pd.DataFrame()

    # Step 1: Retain common columns
    # Rename common columns for clarity
    column_mapping_common = {
        raw_data_df.columns[6]: "ID",  # Participant ID
        raw_data_df.columns[15]: "Mentor or Mentee?",  # Mentor or Mentee
        raw_data_df.columns[11]: "Rank 1",  # First common rank question
        raw_data_df.columns[12]: "Rank 2",  # Second common rank question
        raw_data_df.columns[13]: "Rank 3",  # Third common rank question
        raw_data_df.columns[14]: "Rank 4",  # Fourth common rank question
    }

    raw_data_df = raw_data_df.rename(columns=column_mapping_common)

    # Retain common columns
    # FIXME: Should all the copying be done at the end instead?
    processed_data_df = raw_data_df[
        ["ID", "Mentor or Mentee?", "Rank 1", "Rank 2", "Rank 3", "Rank 4"]
    ]

    # Step 2: Process Mentor and Mentee-specific columns
    mentor_columns = {
        "industry": raw_data_df.columns[16],  # Industry column for mentors
        "rankings": list(raw_data_df.columns[17:19]),  # Additional ranking questions
        "preferences": list(
            raw_data_df.columns[19:34]
        ),  # Preferences for mentors (columns 19-34)
    }

    mentee_columns = {
        "industry": raw_data_df.columns[35],  # Industry column for mentees
        "rankings": list(raw_data_df.columns[36:38]),  # Additional ranking questions
        "preferences": list(
            raw_data_df.columns[38:53]
        ),  # Preferences for mentees (columns 38-53)
    }

    # Separate data for mentors and mentees
    mentors = raw_data_df[raw_data_df["Mentor or Mentee?"] == "Mentor"]
    mentees = raw_data_df[raw_data_df["Mentor or Mentee?"] == "Mentee"]

    # Process Mentor Data
    mentors_processed = mentors[
        ["ID"]
        + mentor_columns["preferences"]
        + ["Rank 1", "Rank 2", "Rank 3", "Rank 4"]
    ]
    mentors_processed = mentors_processed.rename(
        columns={
            col: f"Preference {i+1}"
            for i, col in enumerate(mentor_columns["preferences"])
        }
    )
    mentors_processed["Industry"] = mentors[mentor_columns["industry"]]

    # Process Mentee Data
    mentees_processed = mentees[
        ["ID"]
        + mentee_columns["preferences"]
        + ["Rank 1", "Rank 2", "Rank 3", "Rank 4"]
    ]
    mentees_processed = mentees_processed.rename(
        columns={
            col: f"Preference {i+1}"
            for i, col in enumerate(mentee_columns["preferences"])
        }
    )
    mentees_processed["Industry"] = mentees[mentee_columns["industry"]]

    # Combine the processed data
    processed_data_df = pd.concat(
        [mentors_processed, mentees_processed], ignore_index=True
    )

    # Step 3: Save the processed data to a CSV file
    processed_data_df.to_csv("processed_data.csv", index=False)
    print("Processed data saved to 'processed_data.csv'.")


if __name__ == "__main__":
    # Provide the path to your raw form data CSV file
    process_form_data("matching_responses.csv")
