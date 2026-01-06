export default function Input({ className = "", ...props }) {
  return (
    <input
      className={`border p-2 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500 ${className}`}
      {...props}
    />
  );
}
