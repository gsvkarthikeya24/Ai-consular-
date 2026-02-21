import { useState } from 'react';
import { useNavigate, Link, Navigate } from 'react-router-dom';
import { LogIn, Loader2, GraduationCap } from 'lucide-react';
import api from '../../utils/api';
import { useAuth } from '../../context/AuthContext';
import Card from '../UI/Card';
import Section from '../UI/Section';

const Login = () => {
    const navigate = useNavigate();
    const { authState, login: setAuthLogin } = useAuth();
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    // If already logged in, skip the login page entirely
    if (authState === 'authenticated') {
        return <Navigate to="/dashboard" replace />;
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await api.post('/api/auth/login', formData);
            const { access_token, user } = response.data;

            // Update global auth context (handles localStorage + state update)
            setAuthLogin(access_token, user);
            navigate('/dashboard', { replace: true });
        } catch (err) {
            console.error('Login error:', err.response?.data);
            setError(err.response?.data?.detail || 'Login failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <div className="w-full max-w-md relative z-10">
                {/* Header */}
                <div className="text-center mb-8 animate-fade-in">
                    <div className="inline-flex p-3 bg-gradient-to-br from-primary to-primary-dark rounded-2xl shadow-lg shadow-primary/20 mb-4">
                        <GraduationCap className="w-10 h-10 text-white" />
                    </div>
                    <h1 className="text-4xl font-heading font-bold text-white mb-2 tracking-tight">
                        Welcome Back
                    </h1>
                    <p className="text-text-secondary">
                        Sign in to continue your journey
                    </p>
                </div>

                {/* Login Card */}
                <Card className="animate-slide-up border-primary/10">
                    {error && (
                        <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl">
                            <p className="text-sm text-red-400 text-center">{error}</p>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div className="space-y-1.5">
                            <label className="text-sm font-medium text-text-secondary ml-1">Email</label>
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                className="w-full px-4 py-3 bg-surface-light/50 border border-white/10 rounded-xl text-white placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all"
                                placeholder="name@example.com"
                                required
                            />
                        </div>

                        <div className="space-y-1.5">
                            <label className="text-sm font-medium text-text-secondary ml-1">Password</label>
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                className="w-full px-4 py-3 bg-surface-light/50 border border-white/10 rounded-xl text-white placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all"
                                placeholder="••••••••"
                                required
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-3.5 bg-gradient-to-r from-primary to-primary-dim hover:to-primary text-white font-medium rounded-xl shadow-lg shadow-primary/25 hover:shadow-primary/40 hover:scale-[1.02] active:scale-[0.98] transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed group"
                        >
                            {loading ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <>
                                    <span>Sign In</span>
                                    <LogIn className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                </>
                            )}
                        </button>
                    </form>

                    <div className="mt-8 text-center">
                        <p className="text-sm text-text-muted">
                            Don't have an account?{' '}
                            <Link to="/register" className="text-primary-glow hover:text-white font-medium transition-colors">
                                Create account
                            </Link>
                        </p>
                    </div>
                </Card>
            </div>
        </div>
    );
};

export default Login;
