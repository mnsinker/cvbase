import fs from 'node:fs'
import path from 'node:path'

import { Container } from '@/components/Container'
import { ProjectRenderer } from '../../../components/project/ProjectRenderer'

const JSON_PATH = path.join(
  process.cwd(),
  '../../domains/portfolio/output/cv_base_portfolio_en.json',
)

export default function CVBasePage() {
  const raw = fs.readFileSync(JSON_PATH, 'utf-8')
  const project = JSON.parse(raw)

  return (
    <Container className="mt-16 sm:mt-32">
      <ProjectRenderer project={project} />
    </Container>
  )
}
