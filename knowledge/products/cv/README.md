# Input: 
1. Profile: narratives/job_experiences/profile.md
2. Experience: narratives/job_experiences
3. Projects:
       narratives/job_projects 
        -> build_bullets() 
        -> products/cv/output_bullets


# Phase 1
build_bullets.md:   

    Input:
        job project narrative (one)
        + target role
    
    Output:
        *_bullets.md (one)

# Phase 2
build_consolidated.md: 

    Input: 
        profile.md
            +
        job_experiences/*.md
            +
        project_bullets/*.md
    
    Output:
        Consolidated CV Markdown