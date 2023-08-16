import React from "react";
import { Link } from "react-router-dom";


export const Navbar = () => {
	return (
		<nav className="navtop d-flex align-items-center my-4">
			<div className="container d-flex flex-row justify-content-between align-items-center ">
				<div>
				<Link to="/" className="link-logo">
					<span className="navbar-brand mb-0 h1 ">Lesson Bucket</span>
				</Link>
				</div>
				<div className="ml-auto">
					<Link to="/demo">
						<a className="nav-links mx-4 ">Login</a>
					</Link>
					<Link to="/demo">
						<a className="nav-links mx-4 ">Profile</a>
					</Link>
					<Link to="/demo">
						<a className="nav-links mx-4 ">About us</a>
					</Link>
					<Link to="/demo">
						<a className="nav-links mx-4 ">Pricing</a>
					</Link>
				</div>
			</div>
		</nav>
	);
};
