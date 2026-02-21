import { motion } from 'framer-motion';
import { cn } from '../../utils/cn';

const Card = ({
    children,
    className,
    hover = true,
    hoverable = true, // for backwards compatibility
    glass = true,
    border = true,
    onClick,
    title,
    icon
}) => {
    const Component = onClick ? motion.div : 'div';
    const shouldHover = hover || hoverable;

    return (
        <Component
            onClick={onClick}
            whileHover={shouldHover && onClick ? { scale: 1.01 } : {}}
            className={cn(
                "relative rounded-2xl overflow-hidden transition-all duration-300",
                glass && "bg-surface-light/40 backdrop-blur-md",
                border && "border border-white/5",
                shouldHover && "hover:border-primary-glow/30 hover:shadow-[0_0_20px_rgba(6,182,212,0.15)] group",
                className
            )}
        >
            <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />

            <div className={`relative z-10 ${title ? 'p-0' : 'p-6'}`}>
                {title && (
                    <div className="flex items-center gap-3 p-6 border-b border-white/5">
                        {icon && <div className="p-2 bg-primary/10 rounded-lg">{icon}</div>}
                        <h3 className="text-lg font-bold text-white">{title}</h3>
                    </div>
                )}
                <div className={title ? 'p-6' : ''}>
                    {children}
                </div>
            </div>
        </Component>
    );
};

export default Card;
