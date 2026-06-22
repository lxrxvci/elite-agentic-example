'use client'

import Link from 'next/link'
import { useProjects } from '@/features/projects/api/useProjects'
import { useClients } from '@/features/clients/api/useClients'
import { Button, EmptyState } from '@/shared/ui'

export default function ProjectsPage() {
  const { data: projects, isLoading } = useProjects()
  const { data: clients } = useClients()
  const clientNameById = Object.fromEntries(
    (clients?.items || []).map((c) => [c.id, c.name])
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-elite-text-primary">Projects</h1>
        <Link href="/projects/new">
          <Button>+ Add project</Button>
        </Link>
      </div>

      {isLoading ? (
        <p className="text-elite-text-secondary">Loading…</p>
      ) : projects?.items.length ? (
        <div className="grid gap-4 md:grid-cols-2">
          {projects.items.map((project) => (
            <div
              key={project.id}
              className="rounded-lg border border-elite-border bg-elite-white p-6 shadow-card"
            >
              <h2 className="text-lg font-bold text-elite-text-primary">{project.name}</h2>
              <p className="text-sm text-elite-text-secondary">
                {clientNameById[project.client_id] || project.client_id}
              </p>
              <p className="text-sm text-elite-text-secondary">
                Rounding: {project.rounding_minutes} min
              </p>
            </div>
          ))}
        </div>
      ) : (
        <EmptyState
          title="No projects yet"
          description="Add a project under a client to start tracking time."
          actionLabel="Add project"
          onAction={() => {}}
        />
      )}
    </div>
  )
}
