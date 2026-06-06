'use client';
// Client entry: dynamically load the viewer with SSR disabled — react-three-fiber
// and three touch the DOM, so they must only run on the client. Per Next 16, an
// `ssr:false` dynamic import must live inside a Client Component (this file).
import dynamic from 'next/dynamic';

const ArborViewer = dynamic(() => import('@/components/ArborViewer'), {
  ssr: false,
});

export default function Home() {
  return <ArborViewer />;
}
