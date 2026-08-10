import React from 'react'
import { Eyebrow } from './Components'

interface TableProps {
  children: React.ReactNode
  className?: string
}

export function Table({ children, className = '' }: TableProps) {
  return (
    <div className={`overflow-x-auto ${className}`}>
      <table className="w-full">
        {children}
      </table>
    </div>
  )
}

interface TableHeaderProps {
  children: React.ReactNode
  className?: string
}

export function TableHeader({ children, className = '' }: TableHeaderProps) {
  return (
    <thead className={`bg-canvas-soft ${className}`}>
      {children}
    </thead>
  )
}

interface TableBodyProps {
  children: React.ReactNode
  className?: string
}

export function TableBody({ children, className = '' }: TableBodyProps) {
  return (
    <tbody className={`divide-y divide-hairline ${className}`}>
      {children}
    </tbody>
  )
}

interface TableRowProps {
  children: React.ReactNode
  className?: string
}

export function TableRow({ children, className = '' }: TableRowProps) {
  return (
    <tr className={`hover:bg-canvas-soft transition-colors ${className}`}>
      {children}
    </tr>
  )
}

interface TableHeadProps {
  children: React.ReactNode
  className?: string
}

export function TableHead({ children, className = '' }: TableHeadProps) {
  return (
    <th className={`px-4 py-3 text-left ${className}`}>
      <Eyebrow>{children}</Eyebrow>
    </th>
  )
}

interface TableCellProps {
  children: React.ReactNode
  className?: string
}

export function TableCell({ children, className = '' }: TableCellProps) {
  return (
    <td className={`px-4 py-3 font-body-sm text-ink ${className}`}>
      {children}
    </td>
  )
}
