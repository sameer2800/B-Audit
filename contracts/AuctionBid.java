package com.credits.baudit.contracts;

public class AuctionBid {
	
	private Contractor contractor;
	private long bidPrice;
	
	public AuctionBid(Contractor contractor, long bidPrice) {
		super();
		this.contractor = contractor;
		this.bidPrice = bidPrice;
	}

	public Contractor getContractor() {
		return contractor;
	}

	public void setContractor(Contractor contractor) {
		this.contractor = contractor;
	}

	public long getBidPrice() {
		return bidPrice;
	}

	public void setBidPrice(long bidPrice) {
		this.bidPrice = bidPrice;
	}
	
	
}
