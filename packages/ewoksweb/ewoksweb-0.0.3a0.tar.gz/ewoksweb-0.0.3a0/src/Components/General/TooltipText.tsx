export default function tooltipText(title) {
  return (
    <span
      style={{
        padding: '1px',
        color: 'white',
        fontSize: '0.875rem',
        fontWeight: 300,
        lineHeight: '1.13',
      }}
    >
      <b>{title}</b>
    </span>
  );
}
