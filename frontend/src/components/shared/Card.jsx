const Card = ({ children, className = '', hoverable = false }) => {
    const hoverClass = hoverable ? 'hover:shadow-xl transition-shadow duration-300' : '';

    return (
        <div className={`card ${hoverClass} ${className}`}>
            {children}
        </div>
    );
};

export default Card;
