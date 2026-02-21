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
    // 'loading' | 'authenticated' | 'unauthenticated'
    const [authState, setAuthState] = useState('loading');
    const [currentUser, setCurrentUser] = useState(null);

    const verifySession = useCallback(async () => {
        // Quick client-side check first (no network required)
        if (!isAuthenticated()) {
            setAuthState('unauthenticated');
            setCurrentUser(null);
            return;
        }

        // Verify with backend once on app start
        try {
            const token = getToken();
            const response = await fetch(`${API_URL}/api/auth/profile`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            if (response.ok) {
                const userData = await response.json();
                setCurrentUser(userData);
                // Keep localStorage in sync with latest server data
                setUser(userData);
                setAuthState('authenticated');
            } else {
                // Token rejected — clear stale data
                console.warn('Session invalid — clearing localStorage');
                removeToken();
                removeUser();
                setCurrentUser(null);
                setAuthState('unauthenticated');
            }
        } catch (err) {
            // Network error — trust the local token rather than logging out
            console.warn('Auth check network error, trusting local token:', err.message);
            setCurrentUser(getUser());
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
