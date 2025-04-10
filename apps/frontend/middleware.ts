import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  // Get the pathname of the request
  const path = request.nextUrl.pathname

  // Define public paths that don't require authentication
  const isPublicPath = path === "/login" || path === "/register" || path === "/forgot-password"

  // Check if the user is authenticated by looking for the token cookie
  const token = request.cookies.get("token")?.value || ""

  // Redirect logic
  if (isPublicPath && token) {
    // If user is on a public path but is authenticated, redirect to dashboard
    return NextResponse.redirect(new URL("/dashboard", request.url))
  }

  if (!isPublicPath && !token) {
    // If user is on a protected path but is not authenticated, redirect to login
    return NextResponse.redirect(new URL("/login", request.url))
  }

  return NextResponse.next()
}

// Configure the paths that should trigger this middleware
export const config = {
  matcher: ["/dashboard/:path*", "/profile/:path*", "/login", "/register", "/forgot-password"],
}

