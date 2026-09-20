import { useState } from "react";

const initialProfile = {
  name: "",
  age: "",
  gender: "",
  state: "",
  district: "",
  rural_urban: "Rural",
  category: "",
  annual_income: "",
  occupation: "",
  employment_status: "Employed",
  education_level: "Undergraduate",
  marital_status: "",
  farmer: false,
  land_ownership: false,
  disability: false,
  house_ownership: false,
  bpl_status: false,
  student_status: false,
  street_vendor: false,
  minority: false,
};

function ProfileForm({ initialData = {}, onSubmit, loading = false }) {
  const [profile, setProfile] = useState({
    ...initialProfile,
    ...initialData,
  });

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;

    setProfile((prev) => {
      const updated = {
        ...prev,
        [name]: type === "checkbox" ? checked : value,
      };

      // Smart helper inferences based on occupation
      if (name === "occupation") {
        const lower = value.toLowerCase();
        if (lower.includes("farm")) {
          updated.farmer = true;
          updated.land_ownership = true;
        } else if (lower.includes("student")) {
          updated.student_status = true;
          updated.employment_status = "Student";
        } else if (lower.includes("vendor")) {
          updated.street_vendor = true;
          updated.employment_status = "Self-employed";
        }
      }

      return updated;
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const cleanedProfile = {
      ...profile,
      name: profile.name.trim() || "Citizen",
      age: profile.age === "" ? null : Number(profile.age),
      annual_income:
        profile.annual_income === ""
          ? null
          : Number(profile.annual_income),
    };

    if (onSubmit) {
      onSubmit(cleanedProfile);
    }
  };

  return (
    <form className="profile-form" onSubmit={handleSubmit}>
      <h2>Citizen Profile</h2>
      <p className="form-description">
        Enter your details to find government schemes you may be eligible for.
      </p>

      <div className="form-grid">
        <div className="form-group">
          <label htmlFor="name">Full Name</label>
          <input
            id="name"
            name="name"
            type="text"
            value={profile.name}
            onChange={handleChange}
            placeholder="e.g. Ramesh Kumar"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="age">Age (Years)</label>
          <input
            id="age"
            name="age"
            type="number"
            min="0"
            max="120"
            value={profile.age}
            onChange={handleChange}
            placeholder="e.g. 35"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="gender">Gender</label>
          <select
            id="gender"
            name="gender"
            value={profile.gender}
            onChange={handleChange}
            required
          >
            <option value="">Select gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="state">State / UT</label>
          <input
            id="state"
            name="state"
            type="text"
            value={profile.state}
            onChange={handleChange}
            placeholder="e.g. Uttar Pradesh, Maharashtra"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="district">District</label>
          <input
            id="district"
            name="district"
            type="text"
            value={profile.district}
            onChange={handleChange}
            placeholder="e.g. Varanasi, Pune"
          />
        </div>

        <div className="form-group">
          <label htmlFor="rural_urban">Area of Residence</label>
          <select
            id="rural_urban"
            name="rural_urban"
            value={profile.rural_urban}
            onChange={handleChange}
          >
            <option value="Rural">Rural</option>
            <option value="Urban">Urban</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="category">Social Category</label>
          <select
            id="category"
            name="category"
            value={profile.category}
            onChange={handleChange}
            required
          >
            <option value="">Select category</option>
            <option value="General">General</option>
            <option value="OBC">OBC</option>
            <option value="SC">SC</option>
            <option value="ST">ST</option>
            <option value="EWS">EWS</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="annual_income">Annual Family Income (₹)</label>
          <input
            id="annual_income"
            name="annual_income"
            type="number"
            min="0"
            value={profile.annual_income}
            onChange={handleChange}
            placeholder="e.g. 150000"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="occupation">Primary Occupation</label>
          <input
            id="occupation"
            name="occupation"
            type="text"
            value={profile.occupation}
            onChange={handleChange}
            placeholder="e.g. Farmer, Student, Street Vendor"
          />
        </div>

        <div className="form-group">
          <label htmlFor="employment_status">Employment Status</label>
          <select
            id="employment_status"
            name="employment_status"
            value={profile.employment_status}
            onChange={handleChange}
          >
            <option value="Employed">Employed</option>
            <option value="Self-employed">Self-employed</option>
            <option value="Unemployed">Unemployed</option>
            <option value="Student">Student</option>
            <option value="Retired">Retired</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="education_level">Education Level</label>
          <select
            id="education_level"
            name="education_level"
            value={profile.education_level}
            onChange={handleChange}
          >
            <option value="Undergraduate">Undergraduate</option>
            <option value="Class 11-12">Class 11-12</option>
            <option value="Diploma">Diploma</option>
            <option value="Postgraduate">Postgraduate</option>
            <option value="Secondary">Secondary (Class 10)</option>
            <option value="Primary">Primary</option>
            <option value="None">None</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="marital_status">Marital Status</label>
          <select
            id="marital_status"
            name="marital_status"
            value={profile.marital_status}
            onChange={handleChange}
          >
            <option value="">Select status</option>
            <option value="single">Single</option>
            <option value="married">Married</option>
            <option value="widowed">Widowed</option>
            <option value="divorced">Divorced</option>
          </select>
        </div>
      </div>

      <h3 className="checkbox-section-title">Household & Socio-Economic Indicators</h3>
      <div className="checkbox-grid">
        <label className="checkbox-item">
          <input
            type="checkbox"
            name="farmer"
            checked={profile.farmer}
            onChange={handleChange}
          />
          Farmer / Agricultural worker
        </label>

        <label className="checkbox-item">
          <input
            type="checkbox"
            name="land_ownership"
            checked={profile.land_ownership}
            onChange={handleChange}
          />
          Owns agricultural land
        </label>

        <label className="checkbox-item">
          <input
            type="checkbox"
            name="house_ownership"
            checked={profile.house_ownership}
            onChange={handleChange}
          />
          Owns a permanent (Pucca) house
        </label>

        <label className="checkbox-item">
          <input
            type="checkbox"
            name="bpl_status"
            checked={profile.bpl_status}
            onChange={handleChange}
          />
          Holds BPL (Below Poverty Line) card
        </label>

        <label className="checkbox-item">
          <input
            type="checkbox"
            name="student_status"
            checked={profile.student_status}
            onChange={handleChange}
          />
          Currently enrolled student
        </label>

        <label className="checkbox-item">
          <input
            type="checkbox"
            name="street_vendor"
            checked={profile.street_vendor}
            onChange={handleChange}
          />
          Identified street vendor / hawker
        </label>

        <label className="checkbox-item">
          <input
            type="checkbox"
            name="disability"
            checked={profile.disability}
            onChange={handleChange}
          />
          Person with disability (PwD)
        </label>

        <label className="checkbox-item">
          <input
            type="checkbox"
            name="minority"
            checked={profile.minority}
            onChange={handleChange}
          />
          Belongs to a minority community
        </label>
      </div>

      <button type="submit" disabled={loading}>
        {loading ? "Checking Eligibility..." : "Check My Eligibility"}
      </button>
    </form>
  );
}

export default ProfileForm;