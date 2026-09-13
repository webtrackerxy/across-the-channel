import { lazy, Suspense } from "react";
const Story = lazy(() => import("./StoryPage"));
export default function Entry() {
  const url = new URL(location.href);
  if (url.searchParams.get("view") === "explore") {
    url.searchParams.delete("view");
    if (!url.hash)
      url.hash =
        Number(url.searchParams.get("year")) === 2026
          ? "farther-west"
          : "fuller-picture";
    history.replaceState(null, "", url);
  }
  return (
    <Suspense
      fallback={<p style={{ padding: "2rem" }}>Loading Across the Channel…</p>}
    >
      <Story />
    </Suspense>
  );
}
