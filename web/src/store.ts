import { reactive } from 'vue'

export interface MatchResult {
  name: string
  info: string
  similarity: number
}

export const store = reactive({
  showFilters: false,
  showResult: false,
  toggleFilters() {
    this.showFilters = !this.showFilters
  },
  toggleResult() {
    if (this.matchResult) this.showResult = !this.showResult
  },
  targetImage: null as File | null,
  matchResult: null as MatchResult[] | null,
  selectedResultIndex: 0,
  nextMatch() {
    console.log('nextMatch')
    if (
      this.matchResult &&
      this.selectedResultIndex < this.matchResult?.length - 1
    )
      this.selectedResultIndex++
  },
  previousMatch() {
    console.log('previousMatch')
    if (this.selectedResultIndex > 0) this.selectedResultIndex--
  },
  reset() {
    this.matchResult = null
    this.targetImage = null
  },
  loading: false,
  error: null as string | null,
  clearError() {
    this.error = null
  },
  showInfo: false,
  toggleInfo() {
    console.log(this.showInfo)
    if (this.matchResult) this.showInfo = !this.showInfo
  },
  filters: {
    name: null as string | null,
    gender: 'Homens' as 'Homens' | 'Mulheres',
    category: 'Carro' as 'Carro' | 'Moto',
    checkbox1: false,
    checkbox2: false,
  },
})
