import { Link } from "react-router-dom";
import { ClientRoutes } from "../routes";

export default function Header() {
  return (
    <header className="bg-slate-800 text-gray-100 py-2 px-4">
      <nav>
        <ul className="flex place-content-between">
          <li className="text-4xl uppercase tracking-wider font-bold transition-colors duration-300 hover:text-gray-300 active:text-gray-300">
            <Link to={ClientRoutes.ROOT}>
              <h1 className="inline-block mr-3">Mapply</h1>
              <span className="text-indigo-300">/</span>
              <span className="text-violet-300">/</span>
              <span className="text-purple-300">/</span>
            </Link>
          </li>
          <ul className="flex place-content-between gap-4 items-center">
            <li className="text-lg tracking-wide font-bold transition-colors duration-300 hover:text-gray-300 active:text-gray-300">
              <Link to={ClientRoutes.LOGIN}>Login</Link>
            </li>
            <li className="text-lg tracking-wide font-bold transition-colors duration-300 hover:text-gray-300 active:text-gray-300">
              <Link to={ClientRoutes.SIGNUP}>Sign up</Link>
            </li>
          </ul>
        </ul>
      </nav>
    </header>
  );
}
