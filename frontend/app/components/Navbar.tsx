import Link from 'next/link'
import React from 'react'

const NavBar: React.FC = () => {
  return (
    <nav className="flex justify-between items-center bg-green-950 text-white p-4 px-16">
      <div><img src="../20250406_2319_Image Generation_simple_compose_01jr63j6abfqcad1mxnekhj8pm.png" alt="hello" className='w-28 h-20' /></div>
      <div>
        <Link href="/signin" className="mr-4 hover:text-gray-300">
          Sign In
        </Link>
        <Link href="/signup" className="hover:text-gray-300">
          Sign Up
        </Link>
      </div>
    </nav>
  )
}

export default NavBar
