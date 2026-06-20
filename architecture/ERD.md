# ERD

```mermaid
erDiagram

    EXPERIENCE |o--o{ PROJECT: ""

    EXPERIENCE ||--o| BULLET_FILE: ""

    PROJECT ||--o| BULLET_FILE: ""

    EXPERIENCE {
        string id
        string role
        date start
        date end
    }

    PROJECT {
        string id
        string experience_fk
        date start
        date end
        string status
    }

    BULLET_FILE {
        string project_fk
        string experience_fk
    }
```

* Project: may belong to one Experience.
* Personal projects: do not belong to an Experience.
* Bullet File: 
      may reference: 1 Project or 1 Experience; at least one FK must be populated.

# Inputs of ResumeView

```mermaid
flowchart LR

    Profile
    Experience
    BulletFiles
    RoleProfile

      Profile       --- ResumeView
      Experience    --- ResumeView
      BulletFiles   --- ResumeView
      RoleProfile   --- ResumeView
    
    
```
