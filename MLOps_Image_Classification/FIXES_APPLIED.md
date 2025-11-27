# Fixes Applied to MLOps Image Classification

## Date: November 27, 2025

## Issues Fixed

### 1. ❌ **Low Prediction Confidence (Random Predictions)**
**Problem:** Dog image getting only ~10% confidence for Dog class (should be much higher)

**Root Cause:** Double normalization bug - images were being normalized twice:
- Once in `load_and_preprocess_uploaded_image()` 
- Again in `preprocess_single_image()`

This caused pixel values to be divided by 255 twice, resulting in very small values (0-0.004 instead of 0-1), which the model interpreted as nearly black images, leading to random predictions.

**Fix Applied:**
- Modified `load_and_preprocess_uploaded_image()` to normalize directly and return normalized array with batch dimension
- Updated `preprocess_single_image()` to check if image is already normalized before normalizing again
- Added normalization check in `predict_single_image()` to ensure correct input range

**Files Changed:**
- `src/preprocessing.py` - Lines 73-101
- `src/prediction.py` - Lines 34-51

---

### 2. ❌ **Retraining Fails with Rate Limit Error**
**Problem:** "Rate limit exceeded. Please try again later." when clicking "Start Retraining"

**Root Cause:** Rate limit was set to "1 per hour" which is too restrictive for testing and development.

**Fix Applied:**
- Changed rate limit from `@limiter.limit("1 per hour")` to `@limiter.limit("10 per hour")`
- This allows more testing while still preventing abuse

**Files Changed:**
- `app.py` - Line 468

---

### 3. ❌ **JSON Serialization Errors**
**Problem:** Random JSON errors when saving predictions

**Root Cause:** NumPy data types (numpy.float32, numpy.int64) are not JSON serializable by default.

**Fix Applied:**
- Added robust JSON serialization that converts numpy types to native Python types
- Added validation to check for empty files before parsing JSON
- Added backup mechanism for corrupted persistence files
- Improved error handling to prevent crashes

**Files Changed:**
- `src/prediction.py` - Lines 249-281 (save_to_persistence)
- `src/prediction.py` - Lines 283-304 (load_from_persistence)

---

## Testing the Fixes

### Option 1: Test Locally (if TensorFlow works)

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the app
python app.py

# Open browser to http://localhost:5000
# Upload a dog image and check if confidence is high (>50%)
# Try retraining to see if rate limit is fixed
```

### Option 2: Deploy to Render and Test

```powershell
# Stage the changes
git add src/preprocessing.py src/prediction.py app.py FIXES_APPLIED.md

# Commit the fixes
git commit -m "Fix: Resolve double normalization bug causing random predictions, increase retraining rate limit, add robust JSON error handling"

# Push to trigger Render deployment
git push origin main
```

Wait 3-5 minutes for Render to rebuild, then test at:
https://mlops-image-classification-mwhq.onrender.com

---

## Expected Results After Fix

### ✅ Predictions Should Work Correctly
- **Before:** Dog image → Dog: 10.49%, Airplane: 10.14%, etc. (random)
- **After:** Dog image → Dog: >50%, other classes <5% each

### ✅ Retraining Should Work
- **Before:** "Rate limit exceeded" error immediately
- **After:** Can retrain up to 10 times per hour

### ✅ No JSON Errors
- **Before:** Random crashes or errors saving predictions
- **After:** Graceful handling, corrupted files backed up automatically

---

## Technical Details

### Normalization Flow (Fixed)

**BEFORE (Broken):**
```
Upload → PIL Image → numpy array [0-255]
    → normalize ÷255 → [0-1]
    → normalize ÷255 again → [0-0.004]  ❌ TOO DARK!
    → Model sees nearly black image
    → Random predictions
```

**AFTER (Fixed):**
```
Upload → PIL Image → numpy array [0-255]
    → normalize ÷255 → [0-1]  ✅ CORRECT!
    → Check: already normalized? Yes → skip normalization
    → Model sees correct image
    → Accurate predictions
```

### Rate Limit Comparison

| Endpoint | Before | After |
|----------|--------|-------|
| `/api/predict` | 30/min | 30/min (unchanged) |
| `/api/predict/batch` | 10/min | 10/min (unchanged) |
| `/api/retrain` | 1/hour ❌ | 10/hour ✅ |
| `/api/upload/training-data` | 5/hour | 5/hour (unchanged) |

---

## What Changed in Each File

### `src/preprocessing.py`
1. `load_and_preprocess_uploaded_image()`: Now normalizes directly and returns normalized array
2. `preprocess_single_image()`: Added check to prevent double normalization

### `src/prediction.py`
1. `predict_single_image()`: Added normalization check as final safety net
2. `save_to_persistence()`: Convert numpy types to JSON-safe Python types
3. `load_from_persistence()`: Handle corrupted JSON with backups

### `app.py`
1. `/api/retrain` endpoint: Rate limit increased from 1/hour to 10/hour

---

## Next Steps

1. **Test the fixes** (locally if possible, or deploy to Render)
2. **Verify predictions** are now accurate with higher confidence
3. **Try retraining** to confirm rate limit is fixed
4. **Monitor logs** for any remaining JSON errors (should be gone)

---

## Deployment Command

```bash
# All-in-one command to deploy fixes
git add . ; git commit -m "Fix: prediction accuracy, rate limits, and JSON errors" ; git push origin main
```

Then monitor Render deployment at: https://dashboard.render.com
