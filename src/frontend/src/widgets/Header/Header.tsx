interface HeaderProps {
  title: string
}

export function Header({ title }: HeaderProps) {
  return (
    <header className="border-b pb-4 mb-6">
      <h1 className="text-2xl font-bold">{title}</h1>
    </header>
  )
}
