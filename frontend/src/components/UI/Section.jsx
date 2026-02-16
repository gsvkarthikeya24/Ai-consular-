import React from 'react';
import { cn } from '../../utils/cn';

const Section = ({
    title,
    subtitle,
    children,
    className,
    id,
    fullWidth = false
}) => {
    return (
        <section
            id={id}
            className={cn(
                "py-16 md:py-24 relative overflow-hidden",
                className
            )}
        >
            {/* Background Glow Effect - Optional per section */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-3xl h-64 bg-primary-glow/10 blur-[100px] rounded-full pointer-events-none -z-10" />

            <div className={cn(
                "container mx-auto px-4 md:px-6 relative z-10",
                fullWidth ? "max-w-none" : "max-w-7xl"
            )}>
                {(title || subtitle) && (
                    <div className="mb-12 md:mb-16 text-center max-w-3xl mx-auto">
                        {title && (
                            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-blue-100 to-white pb-2 drop-shadow-lg">
                                {title}
                            </h2>
                        )}
                        {subtitle && (
                            <p className="mt-4 text-lg text-text-secondary leading-relaxed">
                                {subtitle}
                            </p>
                        )}

                        {/* Decorative line */}
                        <div className="mt-6 h-1 w-24 mx-auto bg-gradient-to-r from-transparent via-primary to-transparent rounded-full opacity-70" />
                    </div>
                )}

                <div className="relative">
                    {children}
                </div>
            </div>
        </section>
    );
};

export default Section;
