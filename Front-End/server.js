const express = require("express");
const path = require("path");
const mysql = require("mysql2");
const bcrypt = require("bcrypt");
const session = require("express-session");
const MySQLStore = require("express-mysql-session")(session);

const app = express();
const PORT = process.env.PORT || 3000;

// MySQL DB config
const dbConfig = {
  host: "cougartechdb.cyptvgckm417.us-east-1.rds.amazonaws.com",
  user: "admin",
  password: "cougartech1290",
  database: "ICKYBuffaloBreaks"
};

// Create MySQL connection
const db = mysql.createConnection(dbConfig);

// Connect to DB
db.connect((err) => {
  if (err) {
    console.error("Database connection failed:", err);
  } else {
    console.log("Connected to MySQL database!");
  }
});

// Set up session store
const sessionStore = new MySQLStore(dbConfig);

app.use(
  session({
    secret: "secret-key", // Use a stronger secret in production
    resave: false,
    saveUninitialized: false,
    store: sessionStore,
    cookie: { secure: false } // Set to true if using HTTPS
  })
);

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

// Password helpers
const hashPassword = async (password) => {
  return await bcrypt.hash(password, 10);
};

const verifyPassword = async (password, hashedPassword) => {
  return await bcrypt.compare(password, hashedPassword);
};

// --------------- Routes ------------------

// Home & Static Pages
app.get("/", (req, res) => res.sendFile(path.join(__dirname, "public", "home.html")));
app.get("/signin.html", (req, res) => res.sendFile(path.join(__dirname, "public", "signin.html")));
app.get("/createaccount.html", (req, res) => res.sendFile(path.join(__dirname, "public", "createaccount.html")));
app.get("/aboutpage.html", (req, res) => res.sendFile(path.join(__dirname, "public", "aboutpage.html")));
app.get("/contact.html", (req, res) => res.sendFile(path.join(__dirname, "public", "contact.html")));
app.get("/interestform.html", (req, res) => res.sendFile(path.join(__dirname, "public", "interestform.html")));
app.get("/inventory.html", (req, res) => res.sendFile(path.join(__dirname, "public", "inventory.html")));
app.get("/manage-cards.html", (req, res) => res.sendFile(path.join(__dirname, "public", "manage-cards.html")));
app.get("/admin-welcome.html", (req, res) => res.sendFile(path.join(__dirname, "public", "admin-welcome.html")));
app.get("/interestform-logs.html", (req, res) => res.sendFile(path.join(__dirname, "public", "interestform-logs.html")));


// Register User
app.post("/user", async (req, res) => {
  const { first_name, last_name, email, password, address, city, state, zip } = req.body;

  try {
    const [existingUser] = await db.promise().query("SELECT * FROM Users WHERE email = ?", [email]);
    if (existingUser.length > 0) return res.status(400).send("Email already registered.");

    const hashedPassword = await hashPassword(password);
    const sql = "INSERT INTO Users (first_name, last_name, email, password, address, city, state, zip) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
    await db.promise().query(sql, [first_name, last_name, email, hashedPassword, address, city, state, zip]);

    res.status(201).send("User registration successful!");
  } catch (err) {
    console.error("Registration error:", err);
    res.status(500).send("Server error.");
  }
});

// Login User
app.post("/login", async (req, res) => {
  const { email, password } = req.body;

  try {
    const [users] = await db.promise().query("SELECT * FROM Users WHERE email = ?", [email]);

    if (users.length === 0) {
      console.log("❌ Email not found");
      return res.status(401).send("Invalid email or password.");
    }

    const user = users[0];
    const isMatch = await verifyPassword(password, user.password);

    console.log("Login debug:", {
      inputPassword: password,
      storedHash: user.password,
      isMatch,
      role: user.role
    });

    if (!isMatch) return res.status(401).send("Invalid email or password.");

    req.session.user = {
      id: user.id,
      email: user.email,
      name: user.first_name,
      role: user.role
    };

    const redirect = user.role === "admin" ? "/admin-welcome.html" : "/";
    res.status(200).json({ redirect });

  } catch (err) {
    console.error("Login error:", err);
    res.status(500).send("Server error.");
  }
});



// Check Auth
app.get("/check-auth", (req, res) => {
  if (req.session.user) {
    res.json({ isAuthenticated: true, user: req.session.user });
  } else {
    res.json({ isAuthenticated: false });
  }
});

// Logout
app.get("/logout", (req, res) => {
  req.session.destroy(() => res.redirect("/"));
});

// ----------------- Card CRUD ------------------

// Create Card
app.post("/card", async (req, res) => {
  const { first_name, last_name, team, autograph, price, image_url, additional_specifications } = req.body;

  try {
    const sql = "INSERT INTO Baseball_Cards (first_name, last_name, team, autograph, price, image_url, additional_specifications) VALUES (?, ?, ?, ?, ?, ?, ?)";
    await db.promise().query(sql, [first_name, last_name, team, autograph, price, image_url, additional_specifications]);
    res.status(201).send("Card added successfully!");
  } catch (err) {
    console.error("Add card error:", err);
    res.status(500).send("Error adding card.");
  }
});

// Update Card
app.put("/card", async (req, res) => {
  const { id, team, autograph, price, image_url, additional_specifications } = req.body;

  try {
    const sql = "UPDATE Baseball_Cards SET team = ?, autograph = ?, price = ?, image_url = ?, additional_specifications = ? WHERE id = ?";
    await db.promise().query(sql, [team, autograph, price, image_url, additional_specifications, id]);
    res.status(200).send("Card updated successfully!");
  } catch (err) {
    console.error("Update card error:", err);
    res.status(500).send("Error updating card.");
  }
});

// Delete Card
app.delete("/card", async (req, res) => {
  const { id } = req.body;

  try {
    const sql = "DELETE FROM Baseball_Cards WHERE id = ?";
    await db.promise().query(sql, [id]);
    res.status(200).send("Card deleted successfully!");
  } catch (err) {
    console.error("Delete card error:", err);
    res.status(500).send("Error deleting card.");
  }
});

// Get Single Card by ID
app.get("/card", async (req, res) => {
  const { id } = req.query;

  try {
    const [result] = await db.promise().query("SELECT * FROM Baseball_Cards WHERE id = ?", [id]);
    if (result.length === 0) return res.status(404).send("Card not found.");
    res.json(result[0]);
  } catch (err) {
    console.error("Get card error:", err);
    res.status(500).send("Error fetching card.");
  }
});

// Get All Cards
app.get("/card/all", async (req, res) => {
  try {
    const [cards] = await db.promise().query("SELECT * FROM Baseball_Cards");
    res.json(cards);
  } catch (err) {
    console.error("Get all cards error:", err);
    res.status(500).send("Error fetching cards.");
  }
});


app.post("/interest", async (req, res) => {
  const { name, email, phone, interests, price, cards } = req.body;

  try {
    const sql = `INSERT INTO Interest_Forms (full_name, email, phone, interests, price_offered, cards_selected)
                 VALUES (?, ?, ?, ?, ?, ?)`;

    await db.promise().query(sql, [name, email, phone, interests, price, cards]);
    res.status(201).send("Interest form submitted successfully.");
  } catch (err) {
    console.error("Interest form error:", err);
    res.status(500).send("Error submitting interest form.");
  }
});

app.get("/interest/all", async (req, res) => {
  try {
    const [rows] = await db.promise().query("SELECT * FROM Interest_Forms ORDER BY submitted_at DESC");
    res.json(rows);
  } catch (err) {
    console.error("Fetch logs error:", err);
    res.status(500).send("Error fetching logs.");
  }
});


app.delete("/interest/:id", async (req, res) => {
  const { id } = req.params;
  try {
    await db.promise().query("DELETE FROM Interest_Forms WHERE id = ?", [id]);
    res.sendStatus(200);
  } catch (err) {
    console.error("Delete log error:", err);
    res.status(500).send("Error deleting log.");
  }
});


// Start Server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
