import { Heart } from 'lucide-react';

const Footer = () => {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="fixed bottom-0 left-0 w-full z-40 bg-glass-dark border-t border-white/10 backdrop-blur-xl">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                <div className="flex flex-col sm:flex-row items-center justify-between gap-2">
                    <p className="text-sm text-text-muted text-center sm:text-left">
                        © {currentYear} <span className="text-primary-glow font-semibold">AI Consular</span>. All rights reserved.
                    </p>
                    <p className="text-sm text-text-muted flex items-center gap-1">
                        Made with <Heart className="w-4 h-4 text-red-400 fill-red-400 animate-pulse" /> for students
                    </p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
