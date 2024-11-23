# Some Concerns
- I want to constrain the mentor/mentees preferences to a set list of answers (KIN IDs) to minimize errors in the dataprocessing
- I want to ensure that the mentor/mentee preferences are not repeated

Natively, Microsoft Forms does not support this.

# Some Solutions
- Power Forms
- Create a standalone custom form (TypeScript, React, etc.)
- Google Forms with Add-Ons
  - Form Approvals - kind of like auth, ensures only people in the program's responses count towards the program
  - Dynamic Fields - for easy limiting of responses
  - Choice Eliminator
  - FormFacade for aesthetics
- Typeform
- JotForm
- Airtable + Mini Extensions

Custom App seems like the most viable option.
TypeForm and JotForm are too expensive
Google Forms extensions aren't exactly what we are looking for