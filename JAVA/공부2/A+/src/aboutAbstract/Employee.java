package aboutAbstract;

public abstract class Employee {
	private String first;
	private String last;
	private String ssn;
	public Employee(String first, String last, String ssn) {
		super();
		this.first = first;
		this.last = last;
		this.ssn = ssn;
	}
	public String getFirst() {
		return first;
	}
	public void setFirst(String first) {
		this.first = first;
	}
	public String getLast() {
		return last;
	}
	public void setLast(String last) {
		this.last = last;
	}
	public String getSsn() {
		return ssn;
	}
	public void setSsn(String ssn) {
		this.ssn = ssn;
	}
	@Override
	public String toString() {
		// TODO Auto-generated method stub
		return String.format("%s %s\nssn : %s", getFirst(), getLast(),getSsn());
	}
	
	public abstract double earnings();
	
}
