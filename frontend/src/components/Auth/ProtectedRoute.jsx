import { Navigate } from 'react-router-dom';
import { isAuthenticated, getUser } from '../../utils/auth';

const ProtectedRoute = ({ children, requireAdmin = false }) => {
    if (!isAuthenticated()) {
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
