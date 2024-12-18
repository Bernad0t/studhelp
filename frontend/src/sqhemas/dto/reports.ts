import { Workload } from "../enums/enums"

export interface ReportsDTO{
    id: number
    date_created: Date
    time_reaction: string
    workload: Workload
}