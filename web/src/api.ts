import axios from 'axios'
import { store, type MatchResult } from '@/store'

export async function uploadFile() {
  store.loading = true

  const file = store.targetImage
  const formData = new FormData()

  if (!file) return

  formData.append('file', file)
  formData.append('gender', store.filters.gender)

  if (store.filters.category === 'Moto') {
    formData.append('moto', 'True')
  }

  if (store.filters.checkbox1) {
    formData.append('folders', 'usados 1')
  }

  if (store.filters.checkbox2) {
    formData.append('folders', 'usados 2')
  }

  if (store.filters.name?.length) {
    const names = store.filters.name.split(',')

    for (const name of names) {
      const firstName = name.split(' ')[0]

      formData.append('names', firstName)
    }
  }

  try {
    const response = await axios.post('http://localhost:5000/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    const matchResult: MatchResult[] = (
      response.data as [string, string, number][]
    ).map(e => ({
      name: e[1],
      info: `${e[1].split('.')[0]}.txt`,
      similarity: e[2],
    }))

    store.matchResult = matchResult.sort((a, b) => b.similarity - a.similarity)
  } catch (error) {
    store.error = error as string
  }
}
