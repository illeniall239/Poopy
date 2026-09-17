// The app runs code and drives local models, so only this machine's own pages may talk to it.
// Blocks other websites (cross-origin POSTs) and DNS-rebinding tricks (foreign Host headers).
import { NextResponse, type NextRequest } from "next/server";

const LOCAL_HOSTS = new Set(["127.0.0.1", "localhost", "[::1]"]);

export function proxy(request: NextRequest) {
  const host = request.headers.get("host") ?? "";
  if (!LOCAL_HOSTS.has(host.replace(/:\d+$/, ""))) {
    return new NextResponse("Forbidden: the tutor only answers on localhost.", { status: 403 });
  }
  if (request.method !== "GET" && request.method !== "HEAD") {
    const origin = request.headers.get("origin");
    if (!origin || new URL(origin).host !== host) {
      return new NextResponse("Forbidden: cross-origin request.", { status: 403 });
    }
  }
  return NextResponse.next();
}

export const config = {
  matcher: "/((?!_next/static|_next/image|favicon.ico).*)",
};
