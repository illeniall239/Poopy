import { redirect } from "next/navigation";

// The curriculum lives on Home now; old links to /topics land there.
export default function TopicsIndex() {
  redirect("/");
}
