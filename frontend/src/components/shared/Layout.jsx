import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import BackgroundEffect from '../UI/BackgroundEffect';
import Footer from './Footer';

/**
 * Global Layout component that includes common UI elements 
 * like Navbar, Footer, and Background animations.
 * Centralizing this here prevents state flicker during navigation.
 */
const Layout = () => {
    return (
        <div className="min-h-screen bg-surface flex flex-col">
            <BackgroundEffect />
            <Navbar />
            <main className="flex-grow pt-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
                <Outlet />
            </main>
            <Footer />
        </div>
    );
};

export default Layout;
