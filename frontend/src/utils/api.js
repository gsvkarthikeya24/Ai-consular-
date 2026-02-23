import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        const status = error.response?.status;
        const url = error.config?.url || '';

        // Only auto-logout on 401 when it's NOT:
        // - The login endpoint (expected to get 401 on bad credentials)
        // - The profile-check endpoint (used by ProtectedRoute — it handles the redirect itself)
        const isLoginEndpoint = url.includes('/api/auth/login');
        const isProfileEndpoint = url.includes('/api/auth/profile');

        if (status === 401 && !isLoginEndpoint && !isProfileEndpoint) {
            // Unauthorized - clear token
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');

            // Force a reload to clear all React states and redirect to login
            // but only if we're not already heading there to avoid loops
            if (!window.location.pathname.startsWith('/login') && !window.location.pathname.startsWith('/register')) {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default api;
