package com.credits.baudit.contracts;

public class Contractor {
	private final String contractorName ;
	private final long contractorRatings;
	private final String contractorDetails;
	private long wallet;
	
	public Contractor(String contractorName, long contractorRatings, String contractorDetails) {
		this.contractorName = contractorName;
		this.contractorRatings = contractorRatings;
		this.contractorDetails = contractorDetails;
	}

	public void transfer(long amount) {
		wallet = wallet + amount;
	}
	public String getContractorName() {
		return contractorName;
	}

	public long getContractorRatings() {
		return contractorRatings;
	}

	public String getContractorDetails() {
		return contractorDetails;
	}
	
	
}
