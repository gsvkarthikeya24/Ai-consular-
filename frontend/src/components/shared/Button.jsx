import { cn } from '../../utils/cn';

const Button = ({
    children,
    variant = 'primary',
    size = 'md',
    className,
    loading = false,
    disabled,
    ...props
}) => {
    const baseStyles = "relative inline-flex items-center justify-center font-medium transition-all duration-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed group overflow-hidden";

    const variants = {
        primary: "bg-primary text-white shadow-lg shadow-primary/25 hover:bg-primary-dark hover:shadow-primary/40 hover:scale-[1.02]",
        secondary: "bg-surface-light text-primary border border-white/10 hover:bg-white/5 hover:border-primary/30",
        outline: "border-2 border-primary text-primary hover:bg-primary/10",
        ghost: "text-text-secondary hover:text-white hover:bg-white/5",
        danger: "bg-red-600 text-white hover:bg-red-700 shadow-lg shadow-red-500/20"
    };

    const sizes = {
        sm: "px-3 py-1.5 text-sm",
        md: "px-5 py-2.5 text-sm",
        lg: "px-8 py-3 text-base font-semibold"
    };

    const currentVariant = variants[variant] || variants.primary;

    return (
        <button
            className={cn(
                baseStyles,
                currentVariant,
                sizes[size],
                loading && "cursor-wait opacity-70",
                className
            )}
            disabled={disabled || loading}
            {...props}
        >
            {loading && (
                <div className="mr-2 w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            )}
            <span className="relative z-10 flex items-center justify-center gap-2">
                {children}
            </span>

            {/* Hover Glow Effect for Primary */}
            {!loading && variant === 'primary' && !disabled && (
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000 pointer-events-none" />
            )}
        </button>
    );
};

export default Button;
