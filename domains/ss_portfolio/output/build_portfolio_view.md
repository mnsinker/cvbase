---
name: build_portfolio_view
workflow_type: transformation
transformation_type: full_regeneration

inputs:
  - architecture/project_schema.md
  - content/projects/<project>.md

outputs:
  - content/views/portfolio_views/<project>_portfolio_en.json

read_existing_output: false
compare_existing_output: false
overwrite_output: true

repository_inspection: false
git_operations: false
---

# Purpose

Generate a Portfolio JSON view from a canonical project source.

---

# Inputs

## SOURCE

if SOURCE file is not provided in prompt, throw an error immediately. 


## PROJECT_SCHEMA

Project schema contract.

    architecture/project_schema.md

Rule: 
Do not inspect the repository. This is a closed-book transformation.

    Only read:
    - SOURCE
    - PROJECT_SCHEMA

---

# Output

Generate a json file. 
if file already exists, then overwrite.

    content/views/portfolio_views/<project>_portfolio_en.json

Rule: 

    The final output must be a json file conforming to PROJECT_SCHEMA.
    
    Output files are build artifacts.
    Do not read existing output files.
    Do not compare against existing output files.
    Always regenerate output from source.

---


# Workflow

Execute PROJECT_SCHEMA Steps exactly




