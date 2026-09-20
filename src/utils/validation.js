/*
 * Validation utilities for citizen profile
 */

export function validateRequired(value) {
  return (
    value !== undefined &&
    value !== null &&
    String(value).trim().length > 0
  );
}

export function validateAge(age) {
  if (age === undefined || age === null || age === "") {
    return "Age is required.";
  }

  const numericAge = Number(age);

  if (!Number.isInteger(numericAge)) {
    return "Age must be a whole number.";
  }

  if (numericAge < 0 || numericAge > 120) {
    return "Please enter a valid age.";
  }

  return "";
}

export function validateIncome(income) {
  if (income === undefined || income === null || income === "") {
    return "Annual income is required.";
  }

  const numericIncome = Number(income);

  if (Number.isNaN(numericIncome)) {
    return "Income must be a valid number.";
  }

  if (numericIncome < 0) {
    return "Income cannot be negative.";
  }

  return "";
}

export function validateGender(gender) {
  if (!validateRequired(gender)) {
    return "Gender is required.";
  }

  return "";
}

export function validateCategory(category) {
  if (!validateRequired(category)) {
    return "Category is required.";
  }

  return "";
}

export function validateState(state) {
  if (!validateRequired(state)) {
    return "State is required.";
  }

  return "";
}

export function validateOccupation(occupation) {
  if (!validateRequired(occupation)) {
    return "Occupation is required.";
  }

  return "";
}

/*
 * Validate complete citizen profile
 */
export function validateProfile(profile) {
  const errors = {};

  if (!profile || typeof profile !== "object") {
    return {
      profile: "Invalid profile data.",
    };
  }

  const ageError = validateAge(profile.age);
  if (ageError) {
    errors.age = ageError;
  }

  const incomeError = validateIncome(profile.annual_income);
  if (incomeError) {
    errors.annual_income = incomeError;
  }

  const genderError = validateGender(profile.gender);
  if (genderError) {
    errors.gender = genderError;
  }

  const categoryError = validateCategory(profile.category);
  if (categoryError) {
    errors.category = categoryError;
  }

  const stateError = validateState(profile.state);
  if (stateError) {
    errors.state = stateError;
  }

  const occupationError = validateOccupation(profile.occupation);
  if (occupationError) {
    errors.occupation = occupationError;
  }

  return errors;
}

/*
 * Check whether validation contains errors
 */
export function isValidProfile(profile) {
  return Object.keys(validateProfile(profile)).length === 0;
}

/*
 * Generic form validation helper
 */
export function getFirstValidationError(errors) {
  const keys = Object.keys(errors || {});

  if (keys.length === 0) {
    return null;
  }

  return errors[keys[0]];
}