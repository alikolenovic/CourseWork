monitor IndexedBarrier {
	private Map<String, Int> thresholds;
	private Condition okToPass;

	public boolean newBarrier(aKey, n) {
		if thresholds.keys().contains(aKey) { return false; }
		thresholds.put(aKey, n);
		return true;
	}

	public boolean pass(aKey) {
			if (!thresholds.keys().contains(aKey)) {
				return false;
			}
		
			int c = thresholds.get(aKey);

			if (c > 0) {
				thresholds.set(aKey, c - 1);
				while (thresholds.get(aKey) > 0) {
					okToPass.wait();
				}
				okToPass.signalAll();
			}
		return true;
	}
}