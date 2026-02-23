import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import {
    isAuthenticated,
    getToken,
    getUser,
    setToken,
    setUser,
    removeToken,
    removeUser,
} from '../utils/auth';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const AuthContext = createContext(null);

/**
 * AuthProvider — verifies the token with the backend ONCE on app startup.
 * All routes and components read from this context, so there are no repeated
 * API calls per navigation and no flicker/re-login on back button presses.
 */
export const AuthProvider = ({ children }) => {
    // Initialize state strictly from localStorage for instant auth state on navigation/back
    const initialUser = getUser();
    const initialToken = getToken();
    const isInitiallyAuthed = isAuthenticated();

    // If ANY token is present in localStorage → start authenticated immediately.
    // The background verifySession call will only log out on an explicit 401.
    // This prevents the 'loading' flash that sends the back-button press to /login.
    const [authState, setAuthState] = useState(initialToken ? 'authenticated' : 'unauthenticated');
    const [currentUser, setCurrentUser] = useState(initialUser);

    const verifySession = useCallback(async () => {
        const token = getToken();

        if (!token) {
            setAuthState('unauthenticated');
            setCurrentUser(null);
            return;
        }

        try {
            const response = await fetch(`${API_URL}/api/auth/profile`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            if (response.ok) {
                const userData = await response.json();
                setCurrentUser(userData);
                setUser(userData);
                setAuthState('authenticated');
            } else if (response.status === 401) {
                // Only de-authenticate if the server explicitly rejects the token as unauthorized
                console.warn('Session explicitly invalid — clearing localStorage');
                removeToken();
                removeUser();
                setCurrentUser(null);
                setAuthState('unauthenticated');
            } else {
                // For other server errors (500, etc.), keep the current "authenticated" status
                // and just log a warning. This prevents logouts during server maintenance or crashes.
                console.warn(`Auth check server error (${response.status}), keeping session:`, response.statusText);
                setAuthState('authenticated');
            }
        } catch (err) {
            // Network error — trust the local token
            console.warn('Auth check network error, trusting local token:', err.message);
            setAuthState('authenticated');
        }
    }, []);

    // Run once on app mount
    useEffect(() => {
        verifySession();
    }, [verifySession]);

    /** Call this after a successful login API response */
    const login = (token, user) => {
        setToken(token);
        setUser(user);
        setCurrentUser(user);
        setAuthState('authenticated');
    };

    /** Call this to log the user out from anywhere */
    const logout = () => {
        removeToken();
        removeUser();
        setCurrentUser(null);
        setAuthState('unauthenticated');
        window.location.href = '/login';
    };

    return (
        <AuthContext.Provider
            value={{
                authState,          // 'loading' | 'authenticated' | 'unauthenticated'
                isLoggedIn: authState === 'authenticated',
                currentUser,
                login,
                logout,
                verifySession,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>');
    return ctx;
};
