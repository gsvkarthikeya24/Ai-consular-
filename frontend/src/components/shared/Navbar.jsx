import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
    LayoutDashboard,
    BookOpen,
    Compass,
    GraduationCap,
    FileText,
    Briefcase,
    MessageCircle,
    BarChart3,
    LogOut,
    Menu,
    X
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { cn } from '../../utils/cn';
import Button from './Button';

const Navbar = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { currentUser: user, logout: authLogout, isLoggedIn } = useAuth();
    const [scrolled, setScrolled] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const isActive = (path) => location.pathname === path;

    const handleLogout = () => {
        authLogout();
        // logout function in context already handles redirection
    };

    const navItems = [
        { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
        { path: '/tasks', label: 'Tasks', icon: BookOpen },
        { path: '/career', label: 'Career', icon: Compass },
        { path: '/courses', label: 'Courses', icon: GraduationCap },
        { path: '/resume', label: 'Resume', icon: FileText },
        { path: '/internships', label: 'Internships', icon: Briefcase },
        { path: '/mentor', label: 'AI Mentor', icon: MessageCircle },
        { path: '/gate', label: 'GATE Prep', icon: BarChart3 },
    ];

    return (
        <nav className={cn(
            "fixed top-0 left-0 w-full z-50 transition-all duration-300 border-b",
            scrolled ? "bg-glass-dark border-white/10 shadow-lg backdrop-blur-xl" : "bg-transparent border-transparent"
        )}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-20">
                    {/* Logo */}
                    <Link
                        to={isLoggedIn ? "/dashboard" : "/login"}
                        className="flex items-center space-x-3 group"
                    >
                        <div className="p-2 bg-gradient-to-br from-primary to-primary-dark rounded-xl shadow-lg shadow-primary/20 group-hover:shadow-primary/40 transition-all duration-300">
                            <GraduationCap className="w-6 h-6 text-white" />
                        </div>
                        <span className="text-xl font-heading font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400 group-hover:to-white transition-all">
                            AI Consular
                        </span>
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden lg:flex items-center space-x-1">
                        {navItems.map(({ path, label, icon: Icon }) => (
                            <Link
                                key={path}
                                to={path}
                                className={cn(
                                    "flex items-center space-x-2 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300",
                                    isActive(path)
                                        ? "bg-primary/10 text-primary-glow shadow-[0_0_15px_rgba(6,182,212,0.1)] border border-primary/20"
                                        : "text-text-secondary hover:text-white hover:bg-white/5"
                                )}
                            >
                                <Icon className={cn("w-4 h-4", isActive(path) && "text-primary-glow")} />
                                <span>{label}</span>
                            </Link>
                        ))}
                    </div>

                    {/* User Menu & Mobile Toggle */}
                    <div className="flex items-center space-x-4">
                        <div className="text-right hidden sm:block">
                            <p className="text-sm font-medium text-white">{user?.name}</p>
                            <p className="text-xs text-text-muted">{user?.branch} • Year {user?.year}</p>
                        </div>

                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={handleLogout}
                            className="hidden sm:flex"
                            title="Logout"
                        >
                            <LogOut className="w-5 h-5 text-red-400 hover:text-red-300 transition-colors" />
                        </Button>

                        <button
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                            className="lg:hidden p-2 text-text-secondary hover:text-white transition-colors"
                        >
                            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            {mobileMenuOpen && (
                <div className="lg:hidden absolute top-20 left-0 w-full bg-surface/95 backdrop-blur-xl border-b border-white/10 animate-fade-in">
                    <div className="px-4 py-6 space-y-2">
                        {navItems.map(({ path, label, icon: Icon }) => (
                            <Link
                                key={path}
                                to={path}
                                onClick={() => setMobileMenuOpen(false)}
                                className={cn(
                                    "flex items-center space-x-3 px-4 py-3 rounded-xl text-base font-medium transition-all",
                                    isActive(path)
                                        ? "bg-primary/10 text-primary-glow border border-primary/20"
                                        : "text-text-secondary hover:text-white hover:bg-white/5"
                                )}
                            >
                                <Icon className="w-5 h-5" />
                                <span>{label}</span>
                            </Link>
                        ))}
                        <div className="border-t border-white/10 my-4 pt-4">
                            <div className="flex items-center justify-between px-4">
                                <div>
                                    <p className="text-sm font-medium text-white">{user?.name}</p>
                                    <p className="text-xs text-text-muted">{user?.branch}</p>
                                </div>
                                <Button
                                    variant="danger"
                                    size="sm"
                                    onClick={handleLogout}
                                >
                                    Logout
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </nav>
    );
};

export default Navbar;
