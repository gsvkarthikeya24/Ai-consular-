import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '../../utils/cn';

const Card = ({
    children,
    className,
    hover = true,
    glass = true,
    border = true,
    onClick
}) => {
    const Component = onClick ? motion.div : 'div';

    return (
        <Component
            onClick={onClick}
            whileHover={hover && onClick ? { scale: 1.02 } : {}}
            className={cn(
                "relative rounded-2xl overflow-hidden transition-all duration-300",
                glass && "bg-glass backdrop-blur-md",
                border && "border border-white/5",
                hover && "hover:border-primary-glow/30 hover:shadow-neon-blue group",
                className
            )}
        >
            {/* Inner Glow Gradient */}
            <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />

            <div className="relative z-10 p-6">
                {children}
            </div>
        </Component>
    );
};

export default Card;
