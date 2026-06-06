import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Strict Mode double-mounts components in dev. For a WebGL/react-three-fiber app
  // that means two GL contexts + double scene construction, which is wasteful and can
  // trigger context loss with heavy scenes. Disable it for this viewer.
  reactStrictMode: false,
};

export default nextConfig;
