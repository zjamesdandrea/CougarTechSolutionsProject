const express = require("express");
const path = require("path");
const mysql = require("mysql2");
const bcrypt = require("bcrypt");
const session = require("express-session");

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json()); // Parse JSON body requests
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public"))); // Serve static files

// Session configuration (to track user login)
app.use(
  session({
    secret: "secret-key",
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }, // Change to true in production with HTTPS
  })
);

// 🛠 MySQL Database Connection (Based on Python `creds.py`)
const db = mysql.createConnection({
  host: "cougartechdb.cyptvgckm417.us-east-1.rds.amazonaws.com",
  user: "admin",
  password: "cougartech1290",
  database: "ICKYBuffaloBreaks",
});

// Connect to database
db.connect((err) => {
  if (err) {
    console.error("Database connection failed:", err);
  } else {
    console.log("Connected to MySQL database!");
  }
});

// Hash Password Function (Used for Secure Registration)
const hashPassword = async (password) => {
  return await bcrypt.hash(password, 10);
};

// Verify Password Function (Used for Login)
const verifyPassword = async (password, hashedPassword) => {
  return await bcrypt.compare(password, hashedPassword);
};

// Serve the home page when accessing "/"
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "home.html"));
});

// Serve the Sign-In page
app.get("/signin.html", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "signin.html"));
});

// Serve the Create Account page
app.get("/createaccount.html", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "createaccount.html"));
});

// Register New User
app.post("/user", async (req, res) => {
  const { first_name, last_name, email, password, address, city, state, zip } = req.body;

  try {
    // Check if email already exists
    const [existingUser] = await db.promise().query("SELECT * FROM Users WHERE email = ?", [email]);
    if (existingUser.length > 0) {
      return res.status(400).send("Email already registered.");
    }

    // Hash the password before storing it
    const hashedPassword = await hashPassword(password);

    // Insert new user into the database
    const sql =
      "INSERT INTO Users (first_name, last_name, email, password, address, city, state, zip) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
    await db.promise().query(sql, [first_name, last_name, email, hashedPassword, address, city, state, zip]);

    res.status(201).send("User registration successful!");
  } catch (error) {
    console.error("Error during registration:", error);
    res.status(500).send("Error registering user.");
  }
});

// User Login Route
app.post("/login", async (req, res) => {
  const { email, password } = req.body;

  try {
    // Fetch user from the database
    const [users] = await db.promise().query("SELECT * FROM Users WHERE email = ?", [email]);

    if (users.length === 0) {
      return res.status(401).send("Invalid email or password.");
    }

    const user = users[0];

    // Compare the entered password with the hashed password in the database
    const isMatch = await verifyPassword(password, user.password);
    if (!isMatch) {
      return res.status(401).send("Invalid email or password.");
    }

    // Store user session after successful login
    req.session.user = { id: user.id, email: user.email, name: user.first_name };

    res.status(200).send("Login successful");
  } catch (error) {
    console.error("Error during login:", error);
    res.status(500).send("Internal server error");
  }
});

// Check if User is Logged In
app.get("/check-auth", (req, res) => {
  if (req.session.user) {
    res.json({ isAuthenticated: true, user: req.session.user });
  } else {
    res.json({ isAuthenticated: false });
  }
});

// User Logout Route
app.get("/logout", (req, res) => {
  req.session.destroy(() => {
    res.redirect("/");
  });
});

// Starts the Server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
