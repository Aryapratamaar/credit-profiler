// src/api/http.js
import axios from 'axios'

// Base URL pakai /api supaya lewat proxy Vite (lihat vite.config.js)
export const http = axios.create({
    baseURL: '/api',
    timeout: 15000,
})

// Inject Authorization kalau ada token
http.interceptors.request.use((config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// (Opsional) Tangani 401 di satu tempat
http.interceptors.response.use(
    (res) => res,
    (err) => {
        if (err.response?.status === 401) {
            // contoh paling simpel: hapus token & arahkan ke login
            localStorage.removeItem('accessToken')
            localStorage.removeItem('user')
            // jangan paksa redirect di sini kalau belum ada router; kita tambah nanti
        }
        return Promise.reject(err)
    }
)
