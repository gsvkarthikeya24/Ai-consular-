import { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { isAuthenticated, getToken, getUser, removeToken, removeUser } from '../../utils/auth';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const ProtectedRoute = ({ children, requireAdmin = false }) => {
    const [authState, setAuthState] = useState('loading'); // 'loading' | 'authenticated' | 'unauthenticated'

    useEffect(() => {
        const verifyAuth = async () => {
            // Quick client-side check first
            if (!isAuthenticated()) {
                setAuthState('unauthenticated');
                return;
            }

            // Verify token with backend
            try {
                const token = getToken();
                const response = await fetch(`${API_URL}/api/auth/profile`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });

                if (response.ok) {
                    setAuthState('authenticated');
                } else {
                    // Token rejected by server — clear stale data
                    console.warn('Token rejected by server, clearing session.');
                    removeToken();
                    removeUser();
                    setAuthState('unauthenticated');
                }
            } catch (error) {
                console.error('Auth verification failed:', error);
                // Network error — allow access if token looks valid locally
                // (graceful offline degradation)
                setAuthState('authenticated');
            }
        };

        verifyAuth();
    }, []);

    if (authState === 'loading') {
        return (
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh',
                background: 'linear-gradient(135deg, #0f0c29, #302b63, #24243e)',
                color: '#fff',
                fontSize: '1.2rem',
                fontFamily: 'Inter, sans-serif'
            }}>
                <div style={{ textAlign: 'center' }}>
                    <div style={{
                        width: '40px',
                        height: '40px',
                        border: '3px solid rgba(255,255,255,0.2)',
                        borderTop: '3px solid #8b5cf6',
                        borderRadius: '50%',
                        animation: 'spin 0.8s linear infinite',
                        margin: '0 auto 16px'
                    }} />
                    Verifying session...
                </div>
                <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
            </div>
        );
    }

    if (authState === 'unauthenticated') {
        return <Navigate to="/login" replace />;
    }

    if (requireAdmin) {
        const user = getUser();
        if (user?.role !== 'admin') {
            return <Navigate to="/dashboard" replace />;
        }
    }

    return children;
};

export default ProtectedRoute;
