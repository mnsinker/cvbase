Purpose

    Create a resume inventory from existing assets.

    This is not a software engineering task.
    The task requires collection only.
    Collection means moving existing content into the template.

Read only:

    knowledge/narratives/job_experiences/profile.md
    knowledge/narratives/job_experiences/*
    knowledge/views/project_bullets/*

Variable

    Role
        If omitted: use the first role defined in `architecture/roles.md`

Output

    products/cv/inputs/cv_<role_name>_<yymmdd>.md


Do not:

    - analyze code
    - analyze architecture
    - inspect repository state
    - run git commands
    - perform repository review


Template

    # Summary
        source:
            profile.md
        include: 
            name 
            summary
            education

    # Skills
        source:
            profile.md
        include:
            technical knowledge
            certification


    # Projects
        source:
            project_bullets/*

        include:
            bullet files where:
                project_fk is populated

            - project metadata
            - project bullets

        exclude:
            - front matter
            - evidence mapping

    # Experience
        source:
            experiences/*
            project_bullets/*
        
        sort by: 
            end date descending

        include:
            experience metadata

            bullet files where:
                project_fk is empty
                and experience_fk is populated

            - company information
            - role
            - start date
            - end date
            - description
            - experience bullets

        exclude:
            - front matter
            - evidence mapping


Rules

    - copy existing content only
    - preserve wording
    - preserve ordering

    - do not summarize
    - do not rewrite
    - do not optimize
    - do not remove content
    - do not generate new content

Execution

    Read only:

        profile.md
        experiences/*
        project_bullets/*

    Ignore:

        projects/*
        architecture/*
        skills/*
        views/*
        README.md
        AGENTS.md