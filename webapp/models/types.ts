
export type User = {
  avatarUrl: string
  url: string
  login: string
}

export type Category = 'issue' | 'pullRequest'

export type Comment = {
  author: User
  body: string
  howLongAgo: string
  url: string
}

export type Label = {
  name: string
  color: string
}

export type IssueState = 'OPEN' | 'CLOSED'

export type Issue = {
  assignees: User[]
  author: User
  body: string
  category: Category
  comments: Comment[]
  howLongAgo: string
  labels: Label[]
  number: number
  state: IssueState
  title: string
  url: string
  updatedAt: Date
}

export type PullRequestState = 'OPEN' | 'CLOSED' | 'MERGED'

export type PullRequest = {
  assignees: User[]
  author: User
  body: string
  category: Category
  comments: Comment[]
  howLongAgo: string
  labels: Label[]
  number: number
  state: PullRequestState
  title: string
  url: string
  updatedAt: Date
}

export type Content = Issue | PullRequest

export type TimelineConfig = {
  owner: string
  repo: string
  id: number
}
