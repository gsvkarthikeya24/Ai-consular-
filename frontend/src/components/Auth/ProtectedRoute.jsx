import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Spinner = () => (
    <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        background: 'linear-gradient(135deg, #0f0c29, #302b63, #24243e)',
        color: '#fff',
        fontFamily: 'Inter, sans-serif'
    }}>
        <div style={{ textAlign: 'center' }}>
            <div style={{
                width: '40px',
                height: '40px',
                border: '3px solid rgba(255,255,255,0.15)',
                borderTop: '3px solid #8b5cf6',
                borderRadius: '50%',
                animation: 'spin 0.7s linear infinite',
                margin: '0 auto 16px'
            }} />
            <span style={{ opacity: 0.7, fontSize: '0.95rem' }}>Loading…</span>
        </div>
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
);

/**
 * ProtectedRoute — reads from AuthContext (verified ONCE at app startup).
 * No API call per navigation. Session persists across back/forward navigation.
 */
const ProtectedRoute = ({ children, requireAdmin = false }) => {
    const { authState, currentUser } = useAuth();

    if (authState === 'loading') return <Spinner />;

    if (authState === 'unauthenticated') {
        return <Navigate to="/login" replace />;
    }

    if (requireAdmin && currentUser?.role !== 'admin') {
        return <Navigate to="/dashboard" replace />;
    }

    return children;
};

export default ProtectedRoute;
